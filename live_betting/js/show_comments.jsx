import React from 'react';
import PropTypes from 'prop-types';

class ShowComments extends React.Component {
  constructor(props) {
    super(props);
    this.state = { comments: [] };
  }

  componentDidMount() {
    // Call REST API to get number of likes
    fetch(this.props.url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          comments: data.comments,
        });
      });
  }

  render() {
    const comments = this.state.comments.map(text => (
      <div key={text.commentid} id={text.commentid}><strong>{text.owner}</strong> {text.text}</div>
    ));

    return (
      comments
    );
  }
}

ShowComments.propTypes = {
  url: PropTypes.string.isRequired,
};

export default ShowComments;
