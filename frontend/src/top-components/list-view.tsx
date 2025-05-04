import axios from 'axios'
import { Task_Container } from '../sub-components/task-container'

const get_tasks = async (project_id) => {
	const url = "http://localhost:8000/api/projects/"+project_id+"/tasks";
	try {
		const res = await axios.get(url, {headers: { 'Accept': 'applicaion/json' }});
		return res.data;
	} catch (e) {
		console.error(e);
		return null;
	}
}


const Board_View = (create_task, project_id, res, setRes) => {
	if (!res) {
		const data = async () => {
			const d = await get_tasks(project_id)
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
		switch (task.ColumnID) {
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
		case 5:
			taskse.push(task)
			break;
		}
	}
	
	console.log(tasksb);

	return () => {
		return (
			<>
			<button onClick={() => create_task()}>create task</button>
			<div style={{display: 'flex'}}>
			 <Task_Container tasks={tasksa} />
			 <Task_Container tasks={tasksb} />
			 <Task_Container tasks={tasksc} />
			 <Task_Container tasks={tasksd} />
			 <Task_Container tasks={taskse} />
			</div>
			</>
		)
	}

}

export { Board_View }
