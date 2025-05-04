const Board_Button = ({ title, id, walk }) => {
	console.log(id)
	return (
		<div>
		 <button onClick={() => walk(id)}>{title}</button>
		</div>
	)
}

export { Board_Button }
