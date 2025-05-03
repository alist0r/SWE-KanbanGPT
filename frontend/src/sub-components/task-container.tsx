import { Task_Button } from './task-button';

const Task_Container = ({ tasks }) => {
	return (
		<div>
		{
		 tasks.map((task) => <Task_Button title={task.title} prvRank={task.key} prvCol={0} />)
		}
		</div>
	)
}

export { Task_Container }
