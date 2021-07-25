import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import { Button } from "@material-ui/core";
import { useHistory } from "react-router-dom";

const useStyles = makeStyles((theme) => ({
  linkButton: {
    color: theme.palette.common.white,
    margin: theme.spacing(4),
    height: theme.spacing(10),
    width: theme.spacing(20),
    fontSize: theme.spacing(4),
  },
}));

const LinkButton = (props) => {
  const classes = useStyles();
  const history = useHistory();

  const handleClick = () => {
    history.push(props.to);
  };

  return (
    <Button
      variant="contained"
      color="primary"
      size="large"
      className={classes.linkButton}
      disabled={!props.canVote}
      onClick={handleClick}
    >
      {props.text}
    </Button>
  );
};

export default LinkButton;
