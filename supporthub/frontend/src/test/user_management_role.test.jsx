import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import UserManagement from '../pages/admin/UserManagement';
import { authApi } from '../api/auth';

vi.mock('../api/auth', () => ({
  authApi: {
    listUsers: vi.fn(),
    createUser: vi.fn(),
    updateUser: vi.fn(),
    deleteUser: vi.fn(),
    resetUserPassword: vi.fn(),
  },
}));

describe('UserManagement Role Renaming and Filtering', () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  });

  const mockUsers = [
    { id: '1', name: 'Aarav Sharma', email: 'aarav@example.com', role: 'customer', status: 'active', customer_id: 'CUST-001', phone: '+91-9876543210' },
    { id: '2', name: 'Agent Smith', email: 'agent@supporthub.com', role: 'agent', status: 'active', customer_id: null, phone: null },
    { id: '3', name: 'Admin Boss', email: 'admin@supporthub.com', role: 'admin', status: 'active', customer_id: null, phone: null },
  ];

  it('renders "All Users" tab and role filters properly', async () => {
    authApi.listUsers.mockResolvedValue({ data: mockUsers });

    render(
      <QueryClientProvider client={queryClient}>
        <UserManagement />
      </QueryClientProvider>
    );

    await waitFor(() => {
      // Check that "All Users" text appears in the role filter tabs
      expect(screen.getAllByText(/All Users/i).length).toBeGreaterThan(0);
      expect(screen.getByText('Aarav Sharma')).toBeInTheDocument();
      expect(screen.getByText('Agent Smith')).toBeInTheDocument();
      expect(screen.getByText('Admin Boss')).toBeInTheDocument();
    });
  });
});
