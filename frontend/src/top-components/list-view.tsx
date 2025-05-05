import axios from 'axios'
import { Task_Container } from '../sub-components/task-container'

const get_tasks = async (project_id, setCol) => {
	const url = "http://localhost:8000/api/projects/"+project_id+"/tasks";
	const url2 = "http://localhost:8000/api/projects/"+project_id+"/columns";
	try {
		const res = await axios.get(url, {headers: { 'Accept': 'applicaion/json' }});
		const col = await axios.get(url2, {headers: { 'Accept': 'applicaion/json' }});
		let min = col.data[0].ColumnID
		for (let i = 0; i < col.data.size; ++i) {
			if (min > col.data[i].ColumnID) {
				min = col.data[i].ColumnID;
			}
		}
		setCol(min)
		return res.data;
	} catch (e) {
		console.error(e);
		return null;
	}
}


const Board_View = (create_task, project_id, res, setRes, setCol, walk) => {
	if (!res) {
		const data = async () => {
			const d = await get_tasks(project_id, setCol)
			setRes(d);
		};
		data();
		return () => {<div>loading...</div>};
	}



	const tasksa = [];
	const tasksb = [];
	const tasksc = [];
	const tasksd = [];
	const taskse = [];

	for (let task of res) {
		switch (task.ColumnID % 5) {
		case 1:
			tasksa.push(task)
			break;
		case 2:
			tasksb.push(task)
			break;
		case 3:
			tasksc.push(task)
			break;
		case 4:
			tasksd.push(task)
			break;
		case 0:
			taskse.push(task)
			break;
		}
	}
	
	return () => {
		return (
			<>
			<button onClick={() => create_task()}>create task</button>
			<div style={{display: 'flex'}}>
			 <Task_Container tasks={tasksa} walk={walk} pid={project_id} />
			 <Task_Container tasks={tasksb} walk={walk} pid={project_id} />
			 <Task_Container tasks={tasksc} walk={walk} pid={project_id} />
			 <Task_Container tasks={tasksd} walk={walk} pid={project_id} />
			 <Task_Container tasks={taskse} walk={walk} pid={project_id} />
			</div>
			</>
		)
	}

}

export { Board_View }
