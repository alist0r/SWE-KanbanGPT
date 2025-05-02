import axios from 'axios';
import { useState, useEffect } from 'react'; 
import { Board_Container } from "../sub-components/board-container";

const create_board = () => {
	//TODO make this button goto project creation screen
	return () => {
		return (
			<div>
			 <button>create new project</button>
			</div>
		)
	}
}

const get_projects = async () => {
	//api expects usr id but i dont know how to get that from token, hardcoding here for testing
	const USERID = 2;
	const url: string = "http://localhost:8000/api/users/"+USERID+"/projects";
	try {
		const res = await axios.get(url, {headers: { 'Accept': 'application/json' }})
		return res.data;
	} catch(e) {
		console.error(e)
		return null;
	}
}


const Board_select = (walk_board_view: Function) => {
	const [res, setRes] = useState(null);
	useEffect(() => {
		const data = async () => {
			const d = await get_projects()
			setRes(d);
		};
		data();
	},[]); //??? wtf even is react
	if (!res) {
		return <div>fuck you</div>;
	}
	const New_Project = create_board();
	const token = localStorage.getItem("access_token");
	console.log(token);
	return (
		<>
		 <New_Project />
		 <Board_Container boards={res} />
		</>
	)
}

export { Board_select }
