import React from 'react';
import logo from './logo.svg';
import './App.css';
import { Product } from './interfaces/product'
import { Card, Pagination } from 'react-rainbow-components';
import axios from 'axios';

interface PagingState {
  activePage: number;
  products: Product[],
}

class App extends React.Component<{}, PagingState> {
  constructor(props: any) {
    super(props);
    this.state = {
      activePage: 1,
      products: [],
    };
    this.handleOnChange = this.handleOnChange.bind(this);
    this.loadContents();
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
        key={product.name}
        style={{ width: 240 }}
        className="rainbow-m-bottom_x-large rainbow-m-right_small"
        footer={<span className="rainbow-font-size-text_large rainbow-color_dark-1">{product.name}</span>}
      >
        <div style={{width: '100%', height: 240, backgroundImage: `url(${product.image_url})`, backgroundSize: 'cover'}} />
      </Card>
    ));
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
