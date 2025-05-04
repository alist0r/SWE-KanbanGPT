const Board_Button = ({ title, id, walk }) => {
	return (
		<div>
		 <button onClick={() => walk(id)}>{title}</button>
		</div>
	)
}

export { Board_Button }
