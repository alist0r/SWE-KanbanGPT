import { Board_Button } from './board-button';

const Board_Container = ({ boards }) => {
	console.log(boards);
	return (
		<div>
		{
		 boards.map((board) => <Board_Button title={board} />)
		}
		</div>
	)
}

export { Board_Container }
