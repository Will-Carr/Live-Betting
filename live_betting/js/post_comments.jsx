import React from 'react';
import PropTypes from 'prop-types';

class PostComments extends React.Component {
  constructor(props) {
    super(props);
    this.state = { comments: [] };
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleTextChange = this.handleTextChange.bind(this);
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

  handleTextChange(e) {
    this.setState({ text: e.target.value,
      comments: this.state.comments });
  }

  handleSubmit(e) {
    e.preventDefault();
    const text = this.state.text.trim();
    if (!text) {
      return;
    }

    fetch(this.props.url, { method: 'post',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
      },
      body: JSON.stringify({ text }),
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          comments: this.state.comments.concat(data),
        });
        const outerDiv = document.createElement('DIV');
        const innerStrong = outerDiv.appendChild(document.createElement('STRONG'));
        const owner = document.createTextNode(data.owner);
        innerStrong.appendChild(owner);
        const comment = document.createTextNode(` ${data.text}`);
        outerDiv.appendChild(comment);
        document.getElementById(`/p/${data.postid}/`).appendChild(outerDiv);
      });
  }

  render() {
    return (
      <form id="comment-form" onSubmit={e => this.handleSubmit(e)}>
        <input
          type="text"
          placeholder="Say something..."
          value={this.state.text}
          onChange={e => this.handleTextChange(e)}
        />
        <button type="submit" style={{ display: 'none' }} />
      </form>
    );
  }
}

PostComments.propTypes = {
  url: PropTypes.string.isRequired,
};

export default PostComments;
