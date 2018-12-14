import React from 'react';
import InfiniteScroll from 'react-infinite-scroll-component';
// import PropTypes from 'prop-types';
import Likes from './likes';
import PostComments from './post_comments';
import ShowComments from './show_comments';

class Timeline extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      posts: [],
      url: '/api/v1/p/',
      next: '',
      hasMore: true,
    };
    this.getMorePosts = this.getMorePosts.bind(this);
  }

  componentDidMount() {
    // Call REST API to get number of likes
    // If returning from back button
    if (window.performance.navigation.type === 2) {
      this.state = window.history.state;
      this.componentHelper(this.state);
    } else {
      fetch(this.state.url, { credentials: 'same-origin' })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
          this.state.next = data.next;
          data.results.map(async (postUrl) => {
            fetch(postUrl.url, { credentials: 'same-origin' })
              .then((response) => {
                if (!response.ok) throw Error(response.statusText);
                return response.json();
              })
              .then((dataNew) => {
                this.setState({
                  posts: this.state.posts.concat(dataNew),
                });
                window.history.pushState(this.state, 'history');
              });
          });
        });
      // .catch(error => console.log(error));
    }
  }

  getMorePosts() {
    if (this.state.next === '') {
      this.setState({ hasMore: false });
      return;
    }
    // Get next page
    fetch(this.state.next, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        const curUrl = this.state.next;
        this.setState({
          url: curUrl,
          next: data.next,
        });
        data.results.map(async (postUrl) => {
          fetch(postUrl.url, { credentials: 'same-origin' })
            .then((response) => {
              if (!response.ok) throw Error(response.statusText);
              return response.json();
            })
            .then((dataNew) => {
              const dataCombined = this.state.posts.concat(dataNew);
              this.setState({
                posts: dataCombined,
              });
              window.history.pushState(this.state, 'history');
            });
        });
      });
  }

  componentHelper(state) {
    this.setState(state);
  }

  render() {
    // let posts = this.state.posts.map((post_data) => {
    return (
      <InfiniteScroll
        dataLength={this.state.posts.length}
        next={this.getMorePosts}
        hasMore={this.state.hasMore}
        loader={<h4>Loading...</h4>}
        endMessage=""
      >
        {this.state.posts.map(postData => (
          <div key={postData.post_show_url} className="post">
            <a href={postData.owner_show_url} className="post-header">
              <img src={postData.owner_img_url} alt={postData.owner} className="propic" />
              <strong className="u-slug">{postData.owner}</strong>
            </a>
            <div className="post-header-right">
              <a href={postData.post_show_url} className="timestamp">{postData.age}</a>
            </div>
            <div className="post-img-div">
              <img className="post-img" src={postData.img_url} alt="post" />
            </div>
            <Likes url={`${postData.url}likes/`} />
            <PostComments url={`${postData.url}comments/`} />
            <div id={postData.post_show_url}>
              <ShowComments url={`${postData.url}comments/`} />
            </div>
          </div>
        ))}
      </InfiniteScroll>
    );
  }
}

export default Timeline;
