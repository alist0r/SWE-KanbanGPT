import { useState } from 'react';
import axios from 'axios';

const postCol = (task_id, col, setCol) => {
	const url = "http://localhost:8000/api/tasks/move"
	const token = localStorage.getItem("access_token");
	const json = {"task_id": task_id, "new_column_id": col};
	const headers = {
		headers: {
			Authorization: `Bearer ${token}`
		}
	}
	//unprocessable data? error 422
	axios.put(url, json, headers)
	.then(function (response) {
		console.log(response)
	})
	.catch(function (error) {
		console.error(error)
	});
	setCol(col)
}

const Task_Button = ({title, prvRank, prvCol, id}) => {
	const [rank, setRank] = useState(prvRank);
	const [col, setCol] = useState(prvCol);
	return (
		<div style={{backgroundColor: "red"}}>
		 <input 
		  value={rank} 
		  onChange={e => setRank(e.target.value)} 
		  type='number' 
		  size='1'>
		 </input>
		 <button>{title}</button>
		 <input
		  value={col}
		  onChange={e => postCol(id, e.target.value, setCol)} 
		  type='number'
		  size='1'>
		 </input>
		</div>
	)
}

export { Task_Button }
