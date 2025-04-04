import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { login } from './top-components/login.tsx'
import { create_user } from './top-components/create-user.tsx'
import { create_task } from './top-components/create-task.tsx'

enum Pages {
	login,
	create_user,
	board,
	task,
	make_task
}

const App = () => {
	const [page, setPage] = useState(Pages.login);

	const walk_create_user = () => {
		setPage(Pages.create_user);
	}

	const walk_login = () => {
		setPage(Pages.login);
	}

	const walk_create_task = () => {
		setPage(Pages.make_task);
	}

	let Main = () => {return <></>};
	switch (page) {
		case Pages.login:
			Main = login(walk_create_user, walk_create_task);
			break;
		case Pages.create_user:
			Main = create_user(walk_login);
			break;
		case Pages.board:
			Main = () => {return <></>};
			break;
		case Pages.task:
			Main = () => {return <></>};
			break;
		case Pages.make_task:
			Main = create_task(walk_login);
			break;
	}
	
	return (
		<>
		 <Main />
		</>
	)
}

	export default App
