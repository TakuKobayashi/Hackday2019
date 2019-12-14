import React from 'react';
import logo from './logo.svg';
import './App.css';
import { Product } from './interfaces/product'
import { Card, Pagination } from 'react-rainbow-components';
import axios from 'axios';
import {Button, Modal} from "react-rainbow-components/components";
import linepay_icon from './icons/linepay_logo.png'
const QRCode = require('qrcode.react');

interface ProductsState {
  activePage: number;
  products: Product[],
  isOpen: boolean,
}

class App extends React.Component<{}, ProductsState> {
  constructor(props: any) {
    super(props);
    this.state = {
      activePage: 1,
      products: [],
      isOpen: false,
    };
    this.handleOnChange = this.handleOnChange.bind(this);
    this.loadContents();
    this.handleOnClick = this.handleOnClick.bind(this);
    this.handleOnClose = this.handleOnClose.bind(this);
  }

  async loadContents(): Promise<Product[]> {
    const res = await axios.get(process.env.REACT_APP_API_ROOT_URL + '/api/mst/products')
    this.setState({
      products: res.data,
    });
    return this.state.products;
  }

  getContent() {
    const { activePage } = this.state;
    const lastItem = activePage * 2;
    const firstItem = lastItem - 2;
    return this.state.products.slice(firstItem, lastItem).map((product) => (
      <Card
        title={product.name}
        style={{ width: 240 }}
        className="rainbow-m-bottom_x-large rainbow-m-right_small"
        footer={
          <div>
            <div className="rainbow-font-size-text_large rainbow-color_dark-1">{product.price} {product.currency}</div>
            <Button
              label="購入する"
              onClick={this.handleOnClick}
              variant="brand"
              className="rainbow-m-around_medium"
            />
          </div>
        }
      >
        <div style={{width: '100%', height: 240, backgroundImage: `url(${product.image_url})`, backgroundSize: 'cover'}} />
        <Modal
            id="modal-1"
            title={product.name}
            isOpen={this.state.isOpen}
            onRequestClose={this.handleOnClose}
        >
          <div className="rainbow-align-content_center">
            <img
              src={linepay_icon}
            />
          </div>
          <div>
            <QRCode value={process.env.REACT_APP_API_ROOT_URL + '/pay/product/' + product.id} />
          </div>
        </Modal>
      </Card>
    ));
  }

  handleOnClick() {
    return this.setState({ isOpen: true });
  }

  handleOnClose() {
    return this.setState({ isOpen: false });
  }

  handleOnChange(event: React.MouseEvent<HTMLElement>, page: number) {
    this.setState({ activePage: page });
  }

  render():
    | React.ReactElement<any, string | React.JSXElementConstructor<any>>
    | string
    | number
    | {}
    | React.ReactNodeArray
    | React.ReactPortal
    | boolean
    | null
    | undefined {
    const page = this.state.activePage;
    return (
      <div>
        <div className="rainbow-p-around_xx-large rainbow-align-content_center rainbow-flex_column">
          <div className="rainbow-flex rainbow-justify_space-around rainbow-flex_wrap">{this.getContent()}</div>
          <Pagination className="rainbow-m_auto" pages={6} activePage={page} onChange={this.handleOnChange} />
        </div>
      </div>
    );
  }
}

export default App;
