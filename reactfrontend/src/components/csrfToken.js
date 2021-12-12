import * as React from "react";
export default function CSRFToken(props) {
  return (
    <input type="hidden" name="csrfmiddlewaretoken" value={props.csrftoken} />
  );
}
