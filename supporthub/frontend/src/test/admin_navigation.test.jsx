import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import AdminLayout from '../pages/admin/AdminLayout';

// Mock auth store
vi.mock('../store/authStore', () => ({
  useAuthStore: () => ({
    user: { name: 'Admin User', email: 'admin@supporthub.com', role: 'admin' },
    role: 'admin',
    isAuthenticated: true,
    logout: vi.fn(),
  }),
}));

// Mock child components that might make API calls
vi.mock('../components/AdminHeader', () => ({
  default: () => <div data-testid="admin-header">Admin Header</div>,
}));
vi.mock('../pages/admin/AdminOverview', () => ({
  default: () => <div data-testid="admin-overview">Admin Overview</div>,
}));

describe('Admin Layout & Navigation', () => {
  it('renders all core admin navigation sidebar items', () => {
    render(
      <MemoryRouter initialEntries={['/admin']}>
        <AdminLayout />
      </MemoryRouter>
    );

    expect(screen.getByText('Dashboard')).toBeInTheDocument();
    expect(screen.getByText('User Management')).toBeInTheDocument();
    expect(screen.getByText('Channel Integrations')).toBeInTheDocument();
    expect(screen.getByText('Help Center Management')).toBeInTheDocument();
    expect(screen.getByText('AI Settings')).toBeInTheDocument();
    expect(screen.getByText('Roles & Permissions')).toBeInTheDocument();
    expect(screen.getByText('System Settings')).toBeInTheDocument();
  });

  it('renders Global Inbox with Active, Closed, and All Tickets subpages', () => {
    render(
      <MemoryRouter initialEntries={['/admin']}>
        <AdminLayout />
      </MemoryRouter>
    );

    expect(screen.getByText('Global Inbox')).toBeInTheDocument();
    expect(screen.getByText('Active Tickets')).toBeInTheDocument();
    expect(screen.getByText('Closed Tickets')).toBeInTheDocument();
    expect(screen.getByText('All Tickets')).toBeInTheDocument();
  });
});
