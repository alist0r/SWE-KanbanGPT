import axios from 'axios';
import { useState, useEffect } from 'react'; 
import { Board_Container } from "../sub-components/board-container";

const create_board = (walk_create_board) => {
	return () => {
		return (
			<div>
			 <button onClick={walk_create_board}>create new project</button>
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


const Board_select = (walk_board_view: Function, res: Array, setRes: Function, walk_create_board: Function) => {
	if (!res) {
		const data = async () => {
			const d = await get_projects()
			setRes(d);
		};
		data();
		return () => {<div>loading...</div>};
	}
	const New_Project = create_board(walk_create_board);
	const token = localStorage.getItem("access_token");
	console.log(token);
	return () => {
		return (
			<>
			 <New_Project />
			 <Board_Container boards={res} walk={walk_board_view}/>
			</>
		)
	}
}

export { Board_select }
