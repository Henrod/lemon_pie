import React, { useState } from "react";
import { Box, Button } from "@material-ui/core";
import GoogleLogin from "react-google-login";
import Client from "../api/client";
import { makeStyles } from "@material-ui/core/styles";
import { Redirect } from "react-router-dom";

const useStyles = makeStyles((theme) => ({
  box: {
    position: "absolute",
    left: "50%",
    top: "50%",
    transform: "translate(-50%, -50%)",
  },
  button: {
    fontSize: 20,
  },
}));

const Login = () => {
  const classes = useStyles();
  const client = new Client();
  const [state, setState] = useState({ isLogged: false, henrod: false });

  const handleLogin = async (googleData) => {
    try {
      await client.login(googleData.tokenId);
      setState({ isLogged: true });
    } catch (error) {
      console.log(`error on login: ${error}`);
    }
  };

  return (
    <Box className={classes.box}>
      {state.isLogged && <Redirect to="/" />}
      <GoogleLogin
        className={classes.button}
        render={(renderProps) => (
          <Button
            onClick={renderProps.onClick}
            className={classes.button}
            variant="contained"
            color="primary"
          >
            Log in with Google
          </Button>
        )}
        clientId={process.env.REACT_APP_GOOGLE_CLIENT_ID}
        onSuccess={handleLogin}
        onFailure={handleLogin}
        cookiePolicy={"single_host_origin"}
      />
    </Box>
  );
};

export default Login;
