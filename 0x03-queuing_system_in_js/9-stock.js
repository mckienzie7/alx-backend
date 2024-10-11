#!/usr/bin/node
import express from "express";
import { createClient } from "redis";
import { promisify } from 'util';

const listProducts = [
    {
      itemId: 1,
      itemName: 'Suitcase 250',
      price: 50,
      initialAvailableQuantity: 4
    },
    {
      itemId: 2,
      itemName: 'Suitcase 450',
      price: 100,
      initialAvailableQuantity: 10
    },
    {
      itemId: 3,
      itemName: 'Suitcase 650',
      price: 350,
      initialAvailableQuantity: 2
    },
    {
      itemId: 4,
      itemName: 'Suitcase 1050',
      price: 550,
      initialAvailableQuantity: 5
    },
  ];
  

const getItemById = (id) => {
    const item = listProducts.find(product => product.itemId === id);

    if (item) {
        return item;
    }

    return null;
};

const PORT = 1245;
const app = express();
app.use(express.json());
const client = createClient();

const reserveStockById = async(itemId, stock) => {
    const asyncSet = promisify(client.set).bind(client);
    return await asyncSet(`item.${itemId}`, stock);
};

const getCurrentReservedStockById = async(itemId) => {
    const asyncGet = promisify(client.get).bind(client);
    return await asyncGet(`item.${itemId}`);
};

app.get("/list_products", (req, res) => {
    res.json(listProducts);
});

app.get("/list_products/:itemId", async(req, res) => {
  const { itemId } = req.params;
  const item = getItemById(parseInt(itemId));

  if (item === null) {
    return res.json({ "status":"Product not found" });
  } else {
    const reservedStock = await getCurrentReservedStockById(parseInt(itemId));
    const stock = item.initialAvailableQuantity - parseInt(reservedStock);
    return res.json({ ...item, currentQuantity: stock });
  }
});

app.get("/reserve_product/:itemId", async(req, res) => {
  const itemId = parseInt(req.params.itemId);
  const item = getItemById(parseInt(itemId));

  if (item === null) {
    return res.json({ "status":"Product not found" });
  } 
  const reservedStock = await getCurrentReservedStockById(itemId);

  if (parseInt(reservedStock) >= item.initialAvailableQuantity) {
    return res.json({ status: 'Not enough stock available', itemId });
  }
  await reserveStockById(itemId, parseInt(reservedStock) + 1);
  return res.json({ status: 'Reservation confirmed', itemId });
});

const resetStock = () => {
  const setAsync = promisify(client.set).bind(client);

  return Promise.all(listProducts.map((item) => {
    setAsync(`item.${item.itemId}`, 0);
  }));
}

app.listen(PORT, () => {
  resetStock();
  console.log("Server is istening on port " + PORT);
});
