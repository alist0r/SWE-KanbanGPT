import axios from 'axios'
import { useState } from 'react'

const create_submission_handler = (url: String) => {
	return (formData) => {
		const json = {};
		//placeholder hard coded values
		json["ColumnID"] = 0;
		json["CreatedBy"] = 0;
		formData.forEach((value, key) => {
			json[key] = value;
		});
		console.log(json)
		axios.post(url, json)
		.then(function (response) {
			console.log(response);
		})
		.catch(function (error) {
			console.log(error);
		});
	}
}

const create_task = (swap_screen: Function) => {
	const submission_handler = create_submission_handler("http://localhost:8000/api/tasks");
	return () => {
		return (
			<>
			 <form name="createTask" action={submission_handler}>
			 <label>Title: </label>
			 <input name="title" /><br />
			 <label>Description: </label>
			 <input name="desc" /><br />
			 <button>create!</button>
			 </form>
			 or
			 <br />
			 <button onClick={swap_screen}>return to login</button>
			</>
		)

	}
}

export { create_task }
