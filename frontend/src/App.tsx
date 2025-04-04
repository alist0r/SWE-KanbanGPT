import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { login } from './top-components/login.tsx'
import { create_user } from './top-components/create-user.tsx'

enum Pages {
	login,
	create_user,
	board,
	task
}

function App() {
	const [page, setPage] = useState(Pages.login);

	const walk_create_user = () => {
		setPage(Pages.create_user);
	}

	const walk_login = () => {
		setPage(Pages.login)
	}

	let Main = () => {return <></>};
	switch (page) {
		case Pages.login:
			Main = login(walk_create_user);
			break;
		case Pages.create_user:
			Main = create_user(walk_login);
			break;
		case Pages.board:
			Main = () => {return <></>}
			break;
		case Pages.task:
			Main = () => {return <></>}
			break;
	}
	
	return (
		<>
		 <Main />
		</>
	)
}

	export default App
