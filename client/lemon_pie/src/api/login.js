import { Redirect } from "react-router";

const loginState = (error, state) => ({
  ...state,
  isLogged: ![401, 403].includes(error.response?.status),
});

const redirectComponent = (state) =>
  state.isLogged ? <span /> : <Redirect to="/login" />;

export { loginState, redirectComponent };
