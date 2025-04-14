import axios from 'axios'

const new_button_handler = (f: Function, board_id: int) => {
	return () => {
		f(board_id);
	}
}

const select_board_button = (board_id: int, board_name: string, walk_board_view: Function) => {
	const button_handler = new_button_handler(walk_board_view, board_id);
	return () => {
		return (
			<div>
			 <button onClick={button_handler}>{board_name}</button>
			</div>
		)
	}
}

const create_board = () => {
	return () => {
		return (
			<div>
			 <button>create new project</button>
			</div>
		)
	}
}

const Board_select = (walk_board_view: Function) => {
	const New_Project = create_board();
	const Buttons = ()=> {
		const Button = select_board_button(0, "foo", walk_board_view);
		return (
			<>
			 <Button />
			</>
		)
	}
	//need to get list of boards user can access from database
	//need to be able to create a board
	return () => { 
		return (
			<>
			 <New_Project />
			 <Buttons />
			</>
		)
	}
}

export { Board_select }
