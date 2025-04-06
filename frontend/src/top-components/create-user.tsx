import axios from 'axios'
import { useState } from 'react'


/**
 * This function creates a function that will make a webrequest. The function
 * returned is intended to be used in the html of a react component
 * @param {String} url A string that represents the url of where to make a web
 * 	request
 * @return {Function} A function that makes a web request based off of html
 * 	fields.
 */
const create_submission_handler = (url: String) => {
	return (formData) => {
		const json = {};
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

/**
 * This function creates a react comonent that is swaped with Main in App.tsx.
 * The react component offers a create user functionality for the user
 * @param {Function} swap_screen a 'walk' function that will change the state of Main in
 * 	App.tsx. Used to return to login page
 * @return {Function} a react component that offers create_user functionality.
 */
const create_user = (swap_screen: Function) => {
	const submission_handler = create_submission_handler("http://localhost:8000/api/users");
	return () => {
		return (
			<>
			 <form name="createUser" action={submission_handler}>
			 <label>Username: </label>
			 <input name="username" /><br />
			 <label>Password: </label>
			 <input name="password" /><br />
			 <label>Name: </label>
			 <input name="name" /><br />
			 <label>Email: </label>
			 <input name="email" /><br />
			 <button>create</button>
			 </form>
			 or
			 <br />
			 <button onClick={swap_screen}>return to login</button>
			</>
		)

	}
}

export { create_user }
