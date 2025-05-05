import { Task_Button } from './task-button';

const Task_Container = ({ tasks, walk, pid }) => {
	return (
		<div>
		{
		 tasks.map((task) => <Task_Button title={task.title} prvRank={task.TaskID} prvCol={task.ColumnID} id={task.TaskID} walk={walk} pid={pid} />)
		}
		</div>
	)
}

export { Task_Container }
