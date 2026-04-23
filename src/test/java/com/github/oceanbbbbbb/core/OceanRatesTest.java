package com.github.oceanbbbbbb.core;

import com.github.oceanbbbbbb.bean.Currency;
import org.junit.Test;
import java.math.BigDecimal;
import static org.junit.Assert.*;

public class OceanRatesTest {

    @Test
    public void testGetCoinPrice_BTC_USD() {
        BigDecimal price = OceanRates.getCoinPrice("BTC", Currency.USD);
        assertNotNull("Price should not be null", price);
        assertTrue("Price should be positive", price.compareTo(BigDecimal.ZERO) > 0);
        System.out.println("BTC/USD price: " + price);
    }

    @Test
    public void testGetCoinPrice_BTC_CNY() {
        BigDecimal price = OceanRates.getCoinPrice("BTC", Currency.CNY);
        assertNotNull("Price should not be null", price);
        assertTrue("Price should be positive", price.compareTo(BigDecimal.ZERO) > 0);
        System.out.println("BTC/CNY price: " + price);
    }

    @Test
    public void testGetCoinPrice_ETH_USD() {
        BigDecimal price = OceanRates.getCoinPrice("ETH", Currency.USD);
        assertNotNull("Price should not be null", price);
        assertTrue("Price should be positive", price.compareTo(BigDecimal.ZERO) > 0);
        System.out.println("ETH/USD price: " + price);
    }

    @Test
    public void testGetCoinPrice_BNB_USD() {
        BigDecimal price = OceanRates.getCoinPrice("BNB", Currency.USD);
        assertNotNull("Price should not be null", price);
        assertTrue("Price should be positive", price.compareTo(BigDecimal.ZERO) > 0);
        System.out.println("BNB/USD price: " + price);
    }

    @Test
    public void testGetCoinPrice_UnknownCoin() {
        BigDecimal price = OceanRates.getCoinPrice("UNKNOWN", Currency.USD);
        assertNotNull("Price should not be null even for unknown coin", price);
        assertTrue("Price should be positive", price.compareTo(BigDecimal.ZERO) > 0);
        System.out.println("UNKNOWN/USD price: " + price);
    }
}
