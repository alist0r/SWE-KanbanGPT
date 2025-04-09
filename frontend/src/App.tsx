import { useState } from 'react';
import reactLogo from './assets/react.svg';
import viteLogo from '/vite.svg';
import './App.css';

// Import your components with uppercase names
import { Login } from './top-components/login';  // Renamed login -> Login
import { create_user } from './top-components/create-user'; // Renamed create_user -> CreateUser
import { create_task } from './top-components/create-task'; // Renamed create_task -> CreateTask

enum Pages {
  login,
  create_user,
  board,
  task,
  make_task,
}

/**
 * The app changes definition depending on the state of page.
 * The state of page is changed by various 'walk' functions which traverse
 * what's effectively a finite state machine tree.
 */
const App = () => {
  const [page, setPage] = useState(Pages.login);

  const walk_create_user = () => {
    setPage(Pages.create_user);
  };

  const walk_login = () => {
    setPage(Pages.login);
  };

  const walk_create_task = () => {
    setPage(Pages.make_task);
  };

  // Use a component container that you render based on the current page
  let Main = () => <></>;
  switch (page) {
    case Pages.login:
      Main = () => (
        <Login swap_screen={walk_create_user} swap_screen2={walk_create_task} />
      );
      break;
    case Pages.create_user:
		Main = create_user(walk_login);
      break;
    case Pages.board:
      Main = () => <div>Board Page</div>;
      break;
    case Pages.task:
      Main = () => <div>Task Page</div>;
      break;
    case Pages.make_task:
		Main = create_task(walk_login);
      break;
    default:
      Main = () => <div>Not Found</div>;
  }

  return (
    <div className="App">
      <Main />
    </div>
  );
};

export default App;
