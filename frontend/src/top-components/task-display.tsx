const Task_Display = ({ task_id }) => {
	const url = "http://localhost:8000/api/tasks/ai"
	return () => {
		return (
			<>
			 <label>{title}</label>
			 <label>{desc}</label>
			 <label>{ai_desc}</label>
			</>
		)
	}
}

export { Task_Display }
