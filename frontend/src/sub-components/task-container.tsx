import { Task_Button } from './task-button';

const Task_Container = ({ tasks, walk, pid, walk_task, setCurTask}) => {
	return (
		<div>
		{
		 tasks.map((task) => <Task_Button title={task.title} prvRank={task.TaskID} prvCol={task.ColumnID} id={task.TaskID} walk={walk} pid={pid} walk_task={walk_task} setCurTask={setCurTask} />)
		}
		</div>
	)
}

export { Task_Container }
