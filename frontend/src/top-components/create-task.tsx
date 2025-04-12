import axios from 'axios'
import { useState } from 'react'

const create_submission_handler = (url: string) => {
	return (formData: FormData) => {
	  const json: any = {};
	  // Placeholder values
	  json["ColumnID"] = 1;
	  formData.forEach((value: FormDataEntryValue, key: string) => {
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
	  .then((response) => console.log(response))
	  .catch((error) => console.log(error));
	};
  };
  

const create_task = (swap_screen: () => void) => {
	const submission_handler = create_submission_handler("http://localhost:8000/api/tasks");

	const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
		event.preventDefault();
		const form = event.currentTarget;
		const formData = new FormData(form);
		submission_handler(formData);
	};

	return () => {
		return (
			<>
			 <form name="createTask" action={submission_handler}>
			 <label>Title: </label>
			 <input name="title" /><br />
			 <label>Description: </label>
			 <input name="description" /><br />
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
