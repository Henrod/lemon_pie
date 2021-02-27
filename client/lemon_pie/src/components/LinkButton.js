import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import { Button } from "@material-ui/core";
import { Link } from "react-router-dom";

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

  return (
    <Link
      to={props.to}
      style={{
        textDecoration: "none",
        ...props.style,
      }}
    >
      <Button
        variant="contained"
        color="primary"
        size="large"
        className={classes.linkButton}
      >
        {props.text}
      </Button>
    </Link>
  );
};

export default LinkButton;
