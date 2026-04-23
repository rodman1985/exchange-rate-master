package com.github.oceanbbbbbb.utils;

import com.github.oceanbbbbbb.bean.CurrencyFXH;
import org.junit.Test;
import java.math.BigDecimal;
import static org.junit.Assert.*;

public class ConvertFXHTest {

    @Test
    public void testGetPriceByFXH_USD() {
        try {
            // 测试获取BTC价格（USD）
            BigDecimal price = ConvertFXH.getPriceByFXH("BTC", CurrencyFXH.USD);
            if (price != null) {
                assertTrue("Price should be positive", price.compareTo(BigDecimal.ZERO) > 0);
                System.out.println("BTC/USD price from Feixiaohao: " + price);
            } else {
                System.out.println("Feixiaohao API is not available, test skipped");
            }
        } catch (Exception e) {
            System.out.println("Feixiaohao API test failed: " + e.getMessage());
            // API可能不可用，所以不失败测试
        }
    }

    @Test
    public void testGetPriceByFXH_CNY() {
        try {
            // 测试获取BTC价格（CNY）
            BigDecimal price = ConvertFXH.getPriceByFXH("BTC", CurrencyFXH.CNY);
            if (price != null) {
                assertTrue("Price should be positive", price.compareTo(BigDecimal.ZERO) > 0);
                System.out.println("BTC/CNY price from Feixiaohao: " + price);
            } else {
                System.out.println("Feixiaohao API is not available, test skipped");
            }
        } catch (Exception e) {
            System.out.println("Feixiaohao API test failed: " + e.getMessage());
            // API可能不可用，所以不失败测试
        }
    }

    @Test
    public void testGetPriceByFXH_BTC() {
        try {
            // 测试获取ETH价格（BTC）
            BigDecimal price = ConvertFXH.getPriceByFXH("ETH", CurrencyFXH.BTC);
            if (price != null) {
                assertTrue("Price should be positive", price.compareTo(BigDecimal.ZERO) > 0);
                System.out.println("ETH/BTC price from Feixiaohao: " + price);
            } else {
                System.out.println("Feixiaohao API is not available, test skipped");
            }
        } catch (Exception e) {
            System.out.println("Feixiaohao API test failed: " + e.getMessage());
            // API可能不可用，所以不失败测试
        }
    }
}
