import { useState } from 'react';
import reactLogo from './assets/react.svg';
import viteLogo from '/vite.svg';
import './App.css';

// Import your components with uppercase names
import { Login } from './top-components/login';  // Renamed login -> Login
import { Board_select } from './top-components/board-view';
import { create_user } from './top-components/create-user'; // Renamed create_user -> CreateUser
import { create_task } from './top-components/create-task'; // Renamed create_task -> CreateTask
import { Board_View } from './top-components/list-view';
import { Create_Board } from './top-components/create_board';
import { Task_Display } from './top-components/task-display.tsx';


enum Pages {
  login,
  create_user,
  board_select,
  board_overview,
  make_task,
  create_board
}

/**
 * The app changes definition depending on the state of page.
 * The state of page is changed by various 'walk' functions which traverse
 * what's effectively a finite state machine tree.
 */
const App = () => {
  const [page, setPage] = useState(Pages.login);
  const [board, setBoard] = useState(0);
  const [projects, setProjects] = useState(null)
  const [tasks, setTasks] = useState(null)
  const [col, setCol] = useState(null)
  const [curTask, setCurTask] = useState(0)
  const [desc, setDesc] = useState(null)

  const walk_create_user = () => {
    setPage(Pages.create_user);
  };

  const walk_login = () => {
    setPage(Pages.login);
  };

  const walk_create_task = () => {
    setPage(Pages.make_task);
  };

  const walk_board_select = () => {
    setProjects(null);
    setPage(Pages.board_select);
  }

  const walk_create_board = () => {
    setPage(Pages.create_board);
  }

  const walk_board_view = (board_id: int) => {
    setTasks(null);
    setPage(Pages.board_overview);
    setBoard(board_id);
  }

  const walk_task = () => {
	    setDesc(null);
	  setPage(Pages.task)
  }


  // Use a component container that you render based on the current page
  let Main = () => <></>;
  switch (page) {
    case Pages.login:
      Main = () => (
        <Login create_user={walk_create_user} board_select={walk_board_select} />
      );
      break;
    case Pages.create_user:
		Main = create_user(walk_login);
      break;
    case Pages.board_select:
      Main = Board_select(walk_board_view, projects, setProjects, walk_create_board);
      break;
    case Pages.task:
      Main = () => Task_Display(curTask, desc, setDesc, walk_board_view, board);
      break;
    case Pages.create_board:
      Main = () => Create_Board(walk_board_select);
      break;
    case Pages.make_task:
		Main = create_task(walk_board_view, board, col);
      break;
    case Pages.board_overview:
		Main = Board_View(walk_create_task, board, tasks, setTasks, setCol, walk_board_view, walk_task, setCurTask);
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
