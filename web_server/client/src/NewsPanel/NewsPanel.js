import  './NewsPanel.css';

import Auth from '../Auth/Auth';
import React from 'react';
import NewsCard from '../NewsCard/NewsCard';
import _ from 'lodash';

class NewsPanel extends React.Component {

    constructor() {
        super();
        this.state = {news: null, pageNum: 1, loadedAll: false};
    }

    componentDidMount() {
        this.loadMoreNews();
        this.loadMoreNews = _.debounce(this.loadMoreNews, 1000);
        window.addEventListener('scroll', () => this.handleScroll());
    }

    handleScroll() {
        let scrollY = window.scrollY || window.pageYOffset || document.documentElement.scrollTop;
        if ((window.innerHeight + scrollY) >= (document.body.offsetHeight - 50)) {
            this.loadMoreNews();
        }
    }

    loadMoreNews() {

        if (this.state.loadedAll === true) {
            return;
        }

        const news_url = 'http://' + window.location.hostname + ':3000' +
            '/news/userId/' + Auth.getEmail() + '/pageNum/' + this.state.pageNum;

        const request = new Request(encodeURI(news_url), {
            method: 'GET',
            headers: {
                'Authorization': 'bearer ' + Auth.getToken()
            }
        });

        fetch(request)
            .then(res => res.json())
            .then(news => {
                if (!news || news.length === 0) {
                    this.setState({loadedAll: true});
                } else {
                    this.setState({
                        news: this.state.news ? this.state.news.concat(news) : news,
                        pageNum: this.state.pageNum + 1
                    });
                }
            });
    }

    renderNews() {
        const news_card_list = this.state.news.map((news) => {
            return (
                <a className='list-group-item' href="#">
                    <NewsCard news={news}/>
                </a>
            );
        });

        return (
            <div className='container-fluid'>
                <div className='list-group'>
                    {news_card_list}
                </div>
            </div>
        );
    }

    render() {
        if (this.state.news) {
            return (
                <div>
                    {this.renderNews()}
                </div>
            );
        }
        else {
            return (
                <div id='msg-app-loading'>
                    Loading...
                </div>
            );
        }
    }
}

export default NewsPanel;