import { Task_Button } from './task-button';

const Task_Container = ({ tasks }) => {
	return (
		<div>
		{
		 tasks.map((task) => <Task_Button title={task.title} prvRank={task.TaskID} prvCol={task.ColumnID} />)
		}
		</div>
	)
}

export { Task_Container }
