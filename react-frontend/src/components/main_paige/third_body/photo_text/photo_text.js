import React from 'react';
import './photo_text.css';

class PhotoText extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            img: props.img
        }
        console.log(props.img)
    }
    render() {
        return (
            <div className="photo-text">
                <div className="photo-container">
                    <img src={this.state.img}/>
                </div>
                <div className="text-container">{this.props.text}</div>
            </div>
        );
    }
}

export default PhotoText;
