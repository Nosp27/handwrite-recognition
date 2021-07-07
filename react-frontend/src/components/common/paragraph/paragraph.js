import React from 'react';
import './paragraph.css'

export const Paragraph = ({title, text}) => {
    return <div className={'paragraph'}>
        <div className={'paragraph-title'}>{title.toUpperCase()}</div>
        <div className={'paragraph-text'}>{text}</div>
    </div>
};