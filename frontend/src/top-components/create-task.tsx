import axios from 'axios'
import { useState } from 'react'

const create_submission_handler = (url: string, id) => {
	return (formData) => {
	  const json: any = {};
	  // Placeholder values
	  json["ColumnID"] = id;
	  formData.forEach((value, key) => {
		json[key] = value;
	  });
  
	  // Get token from localStorage
	  const token = localStorage.getItem("access_token");
	  console.log("Token being sent: ", token);

	  axios.post(url, json, {
		headers: {
		  Authorization: `Bearer ${token}`,
		},
	  })
	  .then(function (response) {
		console.log(response);
	  })
	  .catch(function (error) {
		console.log(error);
	  });
	};
  };
  

const create_task = (swap_screen: Function, id: Number) => {
	const submission_handler = create_submission_handler("http://localhost:8000/api/tasks", id);
	return () => {
		return (
			<>
			 <form name="createTask" action={submission_handler}>
			 <label htmlFor="title">Title: </label>
			 <input name="title" id="title" /><br />
			 <label htmlFor="description">Description: </label>
			 <input name="description" id="description" /><br />
			 <button>create!</button>
			 </form>
			 or
			 <br />
			 <button onClick={() => swap_screen(id)}>return to board</button>
			</>
		)

	}
}

export { create_task }
