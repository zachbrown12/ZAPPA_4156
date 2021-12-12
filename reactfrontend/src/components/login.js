import React, { useState } from "react";
import axios from "axios";
import { Navigate } from "react-router-dom";
import { FormControl, Input, InputLabel, Button } from "@mui/material";
import CSRFToken from "./csrfToken";

export default function Login(props) {
  const [password, setPassword] = useState("");

  const onSubmit = (e) => {
    e.preventDefault();

    const user = {
      username: props.username,
      password: password,
    };

    axios
      .post(`/users/login/`, JSON.stringify(user), {
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": props.csrftoken,
        },
      })
      .then((res) => {
        console.log(res.status);
        props.setLoggedIn(true);
      })
      .catch((err) => console.log(err.response.data)); // TODO: Add better error
  };

  return (
    <div>
      {!props.loggedIn ? (
        <div>
          <h1 style={{ margin: "20px" }}>Login User</h1>
          <FormControl
            required={true}
            variant="standard"
            color="primary"
            margin="normal"
            style={{ margin: "20px" }}
          >
            <CSRFToken csrftoken={props.csrftoken} />
            <InputLabel htmlFor="username">Username</InputLabel>
            <Input
              name="username"
              type="username"
              value={props.username}
              required
              onChange={(e) => props.setUsername(e.target.value)}
            />{" "}
          </FormControl>
          <br></br>
          <FormControl
            required={true}
            variant="standard"
            color="primary"
            margin="normal"
            style={{ margin: "20px" }}
          >
            <CSRFToken csrftoken={props.csrftoken} />
            <InputLabel htmlFor="password">Password</InputLabel> <br />
            <Input
              name="password"
              type="password"
              value={password}
              required
              onChange={(e) => setPassword(e.target.value)}
            />{" "}
          </FormControl>
          <br></br>
          <Button
            variant="contained"
            onClick={onSubmit}
            style={{ margin: "20px" }}
          >
            Login
          </Button>
        </div>
      ) : (
        <Navigate to="/games" />
      )}
    </div>
  );
}
