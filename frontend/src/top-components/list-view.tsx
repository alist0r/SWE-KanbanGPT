import { Task_Container } from '../sub-components/task-container'

const Board_View = () => {
	/*
	 * TODO
	 * make query
	 * sort by col
	 * make cols based off query
	 */
	const tasksa = [
		{title: 'foo', desc: 'bar', rank: 1},
		{title: 'baz', desc: 'qux', rank: 2}
	];
	const tasksb = [
		{title: 'quux', desc: 'quuz', rank: 1},
		{title: 'foobar', desc: 'corge', rank: 2}
	];
	const tasksc = [
		{title: 'grault', desc: 'garply', rank: 1},
		{title: 'waldo', desc: 'fred', rank: 2}
	];
	const tasksd = [
		{title: 'xyzzy', desc: 'bar', rank: 1},
		{title: 'thud', desc: 'foo', rank: 2}
	];
	const taskse = [
		{title: 'plugh', desc: 'bar', rank: 1},
		{title: 'toto', desc: 'foo', rank: 2}
	];
	return (
		<div style={{display: 'flex'}}>
		 <Task_Container tasks={tasksa} />
		 <Task_Container tasks={tasksb} />
		 <Task_Container tasks={tasksc} />
		 <Task_Container tasks={tasksd} />
		 <Task_Container tasks={taskse} />
		</div>
	)

}

export { Board_View }
