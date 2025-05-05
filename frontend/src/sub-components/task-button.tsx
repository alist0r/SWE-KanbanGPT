import { useState } from 'react';
import axios from 'axios';

const postCol = (task_id, col, setCol, walk, pid) => {
	const url = "http://localhost:8000/api/tasks/move"
	const token = localStorage.getItem("access_token");
	const json = {"task_id": task_id, "new_column_id": col};
	const headers = {
		headers: {
			Authorization: `Bearer ${token}`
		}
	}
	console.log(typeof(col))
	axios.put(url, json, headers)
	.then(function (response) {
		console.log(response)
	})
	.catch(function (error) {
		console.error(error)
	});
	for(let i = 0; i < 5000; ++i) {} //temp busy wait
	                                 //replace me with async await pattern
	walk(pid);
	setCol(col)
}

const Task_Button = ({title, prvRank, prvCol, id, walk, pid}) => {
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
		  onChange={e => postCol(parseInt(id), parseInt(e.target.value), setCol, walk, pid)} 
		  type='number'
		  size='1'>
		 </input>
		</div>
	)
}

export { Task_Button }
