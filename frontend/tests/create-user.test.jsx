import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import axios from 'axios';

import { create_user } from '../src/top-components/create-user';

vi.mock('axios');

describe('create_user component', () => {
  let mockedPost;

  beforeEach(() => {
    mockedPost = axios.post;
    vi.clearAllMocks();
  });

  it('submits valid form data to the backend', async () => {
    const mockResponse = { data: { message: 'User created successfully', user_id: 1 } };
    mockedPost.mockResolvedValueOnce(mockResponse);

    const swapScreenMock = vi.fn();
    const Component = create_user(swapScreenMock);
    render(<Component />);

    const user = userEvent.setup();

    await user.type(screen.getByLabelText(/username/i, { exact: true }), 'testuser');
    await user.type(screen.getByLabelText(/password/i, { exact: true}), 'P@ssword1');
    await user.type(screen.getByLabelText(/^Name:$/i, { exact: true }), 'Test User');
    await user.type(screen.getByLabelText(/email/i, { exact: true }), 'testuser@example.com');
    await user.click(screen.getByRole('button', { name: /create/i }));

    await waitFor(() => {
      expect(mockedPost).toHaveBeenCalledWith(
        'http://localhost:8000/api/users',
        expect.objectContaining({
          username: 'testuser',
          password: 'P@ssword1',
          name: 'Test User',
          email: 'testuser@example.com',
        })
      );
    });
  });

  it('calls swap_screen when "return to login" is clicked', async () => {
    const swapScreenMock = vi.fn();
    const Component = create_user(swapScreenMock);
    render(<Component />);

    const user = userEvent.setup();
    await user.click(screen.getByRole('button', { name: /return to login/i }));

    expect(swapScreenMock).toHaveBeenCalled();
  });
});
