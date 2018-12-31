import React from 'react';
import PropTypes from 'prop-types';

class Likes extends React.Component {
  /* Display number of likes a like/unlike button for one post
   * Reference on forms https://facebook.github.io/react/docs/forms.html
   */

  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = { num_likes: 0, logname_likes_this: false };
    this.handleSubmit = this.handleSubmit.bind(this);
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
          num_likes: data.likes_count,
          logname_likes_this: data.logname_likes_this,
        });
      })
      .catch(error => console.log(error)); // eslint-disable-line no-console
  }

  likesThis() {
    if (this.state.logname_likes_this) {
      return 'unlike';
    }
    return 'like';
  }

  handleSubmit(e) {
    e.preventDefault();
    let method;
    let newLikes = this.state.num_likes;
    if (this.state.logname_likes_this) {
      method = 'delete';
      newLikes -= 1;
    } else {
      method = 'post';
      newLikes += 1;
    }

    fetch(this.props.url, { method,
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
      },
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
      })
      .then(() => {
        this.setState({
          logname_likes_this: !this.state.logname_likes_this,
          num_likes: newLikes,
        });
      });
    // .catch(error => console.log(error));
  }

  render() {
    // Render number of likes
    const likesThis = this.likesThis();
    return (
      <div className="likes">
        <button id="like-unlike-button" onClick={e => this.handleSubmit(e)}>
          {likesThis}
        </button>
        <p>{this.state.num_likes} like{this.state.num_likes !== 1 ? 's' : ''}</p>
      </div>
    );
  }
}

Likes.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Likes;
