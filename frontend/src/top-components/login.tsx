import React, { useState } from 'react';
import axios from 'axios';

const Login = ({create_user, create_task, board_select}) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  // Handler for submitting the login form
  const handleSubmit = async (event) => {
    event.preventDefault();
  
    // Prepare form data (not JSON)
    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);
  
    try {
      const response = await axios.post('http://localhost:8000/login', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });
  
      console.log('Login response:', response.data);
      setMessage('Login successful!');
      board_select();
      // Save access token!
      localStorage.setItem("access_token", response.data.access_token);
    } catch (error) {
      console.error('Login error:', error);
      setMessage('Login failed. Please check your credentials and try again.');
    }
  };
  

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <label>Username: </label>
        <input
          type="text"
          name="username"
          value={username}
          onChange={(event) => setUsername(event.target.value)}
        />
        <br />
        <label>Password: </label>
        <input
          type="password"
          name="password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
        />
        <br />
        <button type="submit">Login</button>
      </form>
      {message && <p>{message}</p>}
      <br />
      <button onClick={create_user}>Create User</button>
      <button onClick={create_task}>Create Task</button>
    </div>
  );
};

export { Login };
