// tests/CreateTask.test.jsx
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { create_task } from '../src/top-components/create-task';
import axios from 'axios';

vi.mock('axios');

describe('create_task', () => {
  beforeEach(() => {
    localStorage.setItem("access_token", "mock-token-abc");
  });

  it('renders create task form', () => {
    const Component = create_task(() => {});
    render(<Component />);

    expect(screen.getByLabelText(/title/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/description/i)).toBeInTheDocument();
  });

  it('submits form data with token', async () => {
    const user = userEvent.setup();
    const mockedPost = axios.post;
    mockedPost.mockResolvedValueOnce({ data: { success: true } });

    const Component = create_task(() => {});
    render(<Component />);

    await user.type(screen.getByLabelText(/title/i), 'Fix bug');
    await user.type(screen.getByLabelText(/description/i), 'Fix the login bug');

    await user.click(screen.getByRole('button', { name: /create!/i }));

    expect(mockedPost).toHaveBeenCalledWith(
      'http://localhost:8000/api/tasks',
      expect.objectContaining({
        ColumnID: 1,
        title: 'Fix bug',
        description: 'Fix the login bug'
      }),
      expect.objectContaining({
        headers: {
          Authorization: 'Bearer mock-token-abc'
        }
      })
    );
  });

  it('calls swap_screen when return button is clicked', async () => {
    const mockSwap = vi.fn();
    const user = userEvent.setup();

    const Component = create_task(mockSwap);
    render(<Component />);

    await user.click(screen.getByRole('button', { name: /return to login/i }));
    expect(mockSwap).toHaveBeenCalled();
  });
});
