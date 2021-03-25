import React from 'react';
import '../common/site_footer/site_footer.css';
import './recognize_page.css'

class RecognizePage extends React.Component {
    render() {
        return (
            <React.StrictMode>
                <div className="rec-page-container">
                    <div className="white-rect">
                        <div className="text-title">Распознанный текст</div>
                        <div className="text-body">{"sdfsflk\nd\t\ndsf"}</div>
                    </div>
                </div>
            </React.StrictMode>
        );
    }
}

export default RecognizePage;
