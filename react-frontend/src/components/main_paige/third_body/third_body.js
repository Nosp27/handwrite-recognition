import React from 'react';
import PhotoText from "./photo_text/photo_text";

class ThirdBody extends React.Component {
    render() {
        return (
            <section className="third-body-container">
                <div className="tb-header">НАША КОМАНДА</div>
                <div className="tb-photos">
                    <PhotoText text="Першина Анна, аналитик-разработчик" img="/public/TR-logo.jpg"/>
                    <PhotoText text="Ашихмин Павел, бекенд-разработчик" img="Pasha-small.jpg"/>
                    <PhotoText text="Жамгарян Николай, ml-разработчик" img="Kolya-small.jpg"/>
                    <PhotoText text="Карнаухова Алена, фронтенд-разработчик" img="Alena-small.jpg"/>
                </div>
                {/*<div className="tb-photos">*/}
                {/*    <div className="tb-photo-container Anya"></div>*/}
                {/*    <div className="tb-photo-container Pasha"></div>*/}
                {/*    <div className="tb-photo-container Kolya"></div>*/}
                {/*    <div className="tb-photo-container Alena"></div>*/}
                {/*</div>*/}
                {/*<div className="tb-text">Анна Першина, Аналитик-Разработчик</div>*/}
            </section>
        );
    }
}

export default ThirdBody;
