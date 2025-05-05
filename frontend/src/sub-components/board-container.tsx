import { Board_Button } from './board-button';

const Board_Container = ({ boards, walk }) => {
	console.log(boards);
	return (
		<div>
		{
		 boards.map((board) => <Board_Button title={board.title} id={board.project_id} walk={walk} />)
		}
		</div>
	)
}

export { Board_Container }
