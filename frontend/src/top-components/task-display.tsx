import axios from 'axios'

const get_info = async (id) => {
	const url = "http://localhost:8000/api/tasks/ai"
	const token = localStorage.getItem("access_token")
	try {
		const res = await axios.get(url, {params: {task_id: id}})
		return res.data
	} catch (e) {
		console.error(e)
		return null
	}
}


const Task_Display = (task_id, res, setRes, walk, board) => {
	if (!res) {
		const data = async () => {
			const d = await get_info(task_id)
			setRes(d)
		};
		data();
		return () => {<div>loading...</div>};
	}
	return (
		<>
		 <label>Title: </label><label>{res.title}</label><br />
		 <label>Description: </label><label>{res.description}</label><br />
		 <label>AI_Description: </label><label>{res.ai_response}</label><br />
		 <button onClick={() => walk(board)}>return to board</button>

		</>
	)
}

export { Task_Display }
