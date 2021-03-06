import { Button } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import React from "react";
import { useHistory } from "react-router-dom";

const useStyles = makeStyles((theme) => ({
  linkButton: {
    margin: theme.spacing(4),
    height: theme.spacing(10),
    width: theme.spacing(20),
    fontSize: theme.spacing(4),
  },
}));

const LinkButton = ({ to, text, disabled = false }) => {
  const classes = useStyles();
  const history = useHistory();

  const handleClick = () => {
    history.push(to);
  };

  return (
    <Button
      variant="contained"
      color="primary"
      style={{ color: "white" }}
      size="large"
      className={classes.linkButton}
      disabled={disabled}
      onClick={handleClick}
    >
      {text}
    </Button>
  );
};

export default LinkButton;
