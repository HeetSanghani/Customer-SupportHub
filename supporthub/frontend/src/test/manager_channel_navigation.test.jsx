import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { MemoryRouter, useNavigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import ManagerAnalytics from '../pages/manager/ManagerAnalytics';
import UnifiedInbox from '../components/UnifiedInbox';

vi.mock('../store/authStore', () => ({
  useAuthStore: () => ({
    user: { name: 'Manager User', email: 'manager@supporthub.com', role: 'manager' },
    role: 'manager',
    isAuthenticated: true,
    logout: vi.fn(),
  }),
}));

// Mock react-router-dom's useNavigate
const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

// Mock ticketsApi
vi.mock('../api/tickets', () => ({
  ticketsApi: {
    list: vi.fn().mockResolvedValue({
      data: [
        { id: 1, ref: 'TICK-001', subject: 'Chat issue', channel: 'website_chat', status: 'open' },
        { id: 2, ref: 'TICK-002', subject: 'Instagram DM', channel: 'instagram', status: 'open' },
      ],
    }),
  },
}));

// Mock client
vi.mock('../api/client', () => ({
  default: {
    get: vi.fn().mockResolvedValue({ data: [] }),
  },
}));

describe('Manager Volume by Channel Navigation & Filter', () => {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });

  it('Volume by Channel box redirects with specific channel query param on click', async () => {
    render(
      <QueryClientProvider client={queryClient}>
        <MemoryRouter initialEntries={['/manager/analytics']}>
          <ManagerAnalytics />
        </MemoryRouter>
      </QueryClientProvider>
    );

    // Wait for channel cards to render
    const websiteChatCard = await screen.findByText(/WEBSITE CHAT/i);
    expect(websiteChatCard).toBeInTheDocument();

    // Click on website chat card
    fireEvent.click(websiteChatCard.closest('div'));

    // Should navigate to /manager/inbox/all?channel=website_chat
    expect(mockNavigate).toHaveBeenCalledWith('/manager/inbox/all?channel=website_chat');
  });

  it('UnifiedInbox filters tickets based on channel query param', async () => {
    render(
      <QueryClientProvider client={queryClient}>
        <MemoryRouter initialEntries={['/manager/inbox/all?channel=website_chat']}>
          <UnifiedInbox filter="all" basePath="/manager" />
        </MemoryRouter>
      </QueryClientProvider>
    );

    // Should show website_chat ticket and not instagram ticket
    expect(await screen.findByText('Chat issue')).toBeInTheDocument();
    expect(screen.queryByText('Instagram DM')).not.toBeInTheDocument();
  });
});
