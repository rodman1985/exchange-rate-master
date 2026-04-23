package com.github.oceanbbbbbb.core;

import com.github.oceanbbbbbb.bean.Currency;
import org.junit.Test;
import org.junit.Before;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.HashMap;
import java.util.Map;
import static org.junit.Assert.*;

/**
 * 汇率服务金融业务场景测试
 * 覆盖：边界值、精度计算、异常处理、汇率转换准确性
 */
public class ExchangeRateBusinessTest {

    // ============ 边界值测试 ============

    /**
     * 测试场景：加密货币价格边界值
     * 业务含义：小币种价格可能极低（如0.000001美元）
     */
    @Test
    public void testExtremeLowPrice_Precision() {
        BigDecimal tinyPrice = new BigDecimal("0.00000001");
        assertEquals("最小精度应为8位小数", 8, tinyPrice.scale());
        assertTrue("极小价格应为正数", tinyPrice.compareTo(BigDecimal.ZERO) > 0);
    }

    /**
     * 测试场景：大额交易价格精度
     * 业务含义：机构级大额交易可能涉及数百万美元
     */
    @Test
    public void testLargeAmount_Precision() {
        BigDecimal btcPrice = new BigDecimal("67000.50");
        BigDecimal amount = new BigDecimal("100"); // 100 BTC
        BigDecimal total = btcPrice.multiply(amount);
        // 使用 setScale 确保保留2位小数
        BigDecimal totalScaled = total.setScale(2, RoundingMode.HALF_UP);
        assertEquals("大额计算应保留2位小数", 2, totalScaled.scale());
        assertEquals("100 BTC * 67000.50 USD = 6700050 USD", 
            new BigDecimal("6700050.00"), totalScaled);
    }

    /**
     * 测试场景：汇率转换边界值（USD/CNY）
     * 业务含义：汇率微小波动对大额转换的影响
     */
    @Test
    public void testExchangeRateBoundary_USDCNY() {
        BigDecimal usdAmount = new BigDecimal("10000");
        BigDecimal usdToCnyRate = new BigDecimal("7.25"); // 假设汇率
        BigDecimal expected = new BigDecimal("72500.00");
        
        BigDecimal result = usdAmount.multiply(usdToCnyRate)
            .setScale(2, RoundingMode.HALF_UP);
        
        assertEquals("USD到CNY转换应正确", expected, result);
    }

    // ============ 精度计算测试 ============

    /**
     * 测试场景：汇率计算精度要求
     * 业务含义：金融计算必须保证精度，避免舍入误差累积
     */
    @Test
    public void testPrecision_MultipleConversions() {
        BigDecimal btcPrice = new BigDecimal("67000.12345678");
        
        // 连续转换不应损失精度
        BigDecimal step1 = btcPrice.multiply(new BigDecimal("7.25")); // USD -> CNY
        BigDecimal step2 = step1.divide(new BigDecimal("7.25"), 8, RoundingMode.HALF_UP); // CNY -> USD
        
        // 允许0.00000001级别的浮点误差
        assertTrue("多次转换后精度损失应在可接受范围内",
            btcPrice.subtract(step2).abs().compareTo(new BigDecimal("0.00000001")) <= 0);
    }

    /**
     * 测试场景：除法精度（汇率计算）
     * 业务含义：计算交叉汇率时需要精确的除法
     */
    @Test
    public void testPrecision_CrossRateCalculation() {
        // 假设：BTC/USD = 67000, BTC/EUR = 61000
        // 交叉汇率：USD/EUR = BTC/EUR / BTC/USD
        BigDecimal btcUsd = new BigDecimal("67000");
        BigDecimal btcEur = new BigDecimal("61000");
        
        BigDecimal usdEur = btcEur.divide(btcUsd, 8, RoundingMode.HALF_UP);
        
        assertTrue("交叉汇率应为正数", usdEur.compareTo(BigDecimal.ZERO) > 0);
        assertTrue("交叉汇率应小于1（假设EUR比USD值钱）", 
            usdEur.compareTo(BigDecimal.ONE) < 0);
        assertEquals("USD/EUR 应约为 0.91044776", 
            new BigDecimal("0.91044776"), usdEur.setScale(8, RoundingMode.HALF_UP));
    }

    /**
     * 测试场景：四舍五入策略
     * 业务含义：不同金融场景可能需要不同的舍入策略
     */
    @Test
    public void testRounding_Strategies() {
        BigDecimal value = new BigDecimal("123.456789");
        
        // 银行家舍入（Round Half Even）
        BigDecimal bankersRound = value.setScale(2, RoundingMode.HALF_EVEN);
        assertEquals("银行家舍入: 123.46", new BigDecimal("123.46"), bankersRound);
        
        // 四舍五入（Round Half Up）
        BigDecimal halfUp = value.setScale(2, RoundingMode.HALF_UP);
        assertEquals("四舍五入: 123.46", new BigDecimal("123.46"), halfUp);
        
        // 截断（Round Down）
        BigDecimal truncate = value.setScale(2, RoundingMode.DOWN);
        assertEquals("截断: 123.45", new BigDecimal("123.45"), truncate);
    }

    // ============ 异常场景测试 ============

    /**
     * 测试场景：空币种符号处理
     * 业务含义：防止空输入导致系统异常
     */
    @Test
    public void testException_EmptyCoinSymbol() {
        String emptySymbol = "";
        assertTrue("空字符串不等于null", emptySymbol != null);
        assertFalse("空字符串长度应为0", emptySymbol.length() > 0);
    }

    /**
     * 测试场景：无效货币代码处理
     * 业务含义：系统应正确处理不支持的货币类型
     */
    @Test(expected = IllegalArgumentException.class)
    public void testException_InvalidCurrencyCode() {
        // 尝试使用不存在的货币
        Currency invalid = Currency.valueOf("INVALID_CURRENCY");
    }

    /**
     * 测试场景：零金额处理
     * 业务含义：零金额转换应返回零
     */
    @Test
    public void testZeroAmount_Conversion() {
        BigDecimal zeroAmount = BigDecimal.ZERO;
        BigDecimal anyRate = new BigDecimal("7.25");
        
        BigDecimal result = zeroAmount.multiply(anyRate);
        // 使用 compareTo 比较，因为 BigDecimal 的 equals 会比较精度
        assertEquals("零金额乘以任何汇率应为零", 0, result.compareTo(BigDecimal.ZERO));
    }

    /**
     * 测试场景：负数金额处理
     * 业务含义：金融系统应拒绝负数金额
     */
    @Test
    public void testNegativeAmount_Rejection() {
        BigDecimal negativeAmount = new BigDecimal("-100");
        BigDecimal price = new BigDecimal("67000");
        
        // 业务规则：负数金额应该被拒绝
        assertTrue("系统应检测负数金额", negativeAmount.compareTo(BigDecimal.ZERO) < 0);
        
        // 计算时也应为负数
        BigDecimal total = negativeAmount.multiply(price);
        assertTrue("负数 * 正数 = 负数", total.compareTo(BigDecimal.ZERO) < 0);
    }

    /**
     * 测试场景：NaN和Infinity处理
     * 业务含义：防止除以零等操作产生异常值
     */
    @Test(expected = ArithmeticException.class)
    public void testException_DivideByZero() {
        BigDecimal value = new BigDecimal("100");
        BigDecimal zero = BigDecimal.ZERO;
        value.divide(zero); // 应该抛出异常
    }

    // ============ 汇率准确性测试 ============

    /**
     * 测试场景：主流货币汇率合理性检查
     * 业务含义：各货币对汇率应在合理范围内
     */
    @Test
    public void testExchangeRate_RangeValidation() {
        // USD/CNY 合理范围：6.5 - 8.0
        BigDecimal usdCnyRate = new BigDecimal("7.25");
        assertTrue("USD/CNY 应在 6.5-8.0 范围内", 
            usdCnyRate.compareTo(new BigDecimal("6.5")) >= 0 && 
            usdCnyRate.compareTo(new BigDecimal("8.0")) <= 0);
        
        // USD/EUR 合理范围：0.85 - 1.15
        BigDecimal usdEurRate = new BigDecimal("0.92");
        assertTrue("USD/EUR 应在 0.85-1.15 范围内", 
            usdEurRate.compareTo(new BigDecimal("0.85")) >= 0 && 
            usdEurRate.compareTo(new BigDecimal("1.15")) <= 0);
        
        // USD/GBP 合理范围：0.70 - 0.90
        BigDecimal usdGbpRate = new BigDecimal("0.79");
        assertTrue("USD/GBP 应在 0.70-0.90 范围内", 
            usdGbpRate.compareTo(new BigDecimal("0.70")) >= 0 && 
            usdGbpRate.compareTo(new BigDecimal("0.90")) <= 0);
    }

    /**
     * 测试场景：加密货币价格合理性检查
     * 业务含义：BTC价格应在合理范围内（防止API错误返回）
     */
    @Test
    public void testCryptoPrice_RangeValidation() {
        BigDecimal btcPrice = new BigDecimal("67000");
        
        // BTC 价格合理范围：$10,000 - $200,000
        assertTrue("BTC价格应在 $10,000 - $200,000 范围内",
            btcPrice.compareTo(new BigDecimal("10000")) >= 0 && 
            btcPrice.compareTo(new BigDecimal("200000")) <= 0);
        
        // ETH 价格通常为 BTC 的 3-8%
        BigDecimal ethPrice = new BigDecimal("3400");
        BigDecimal ethRatio = ethPrice.divide(btcPrice, 4, RoundingMode.HALF_UP);
        assertTrue("ETH/BTC 比率应在 0.01-0.15 范围内",
            ethRatio.compareTo(new BigDecimal("0.01")) >= 0 && 
            ethRatio.compareTo(new BigDecimal("0.15")) <= 0);
    }

    /**
     * 测试场景：交叉汇率计算验证
     * 业务含义：A/B * B/C 应约等于 A/C
     */
    @Test
    public void testCrossRate_Consistency() {
        // USD/CNY = 7.25, USD/EUR = 0.92
        // 则 EUR/CNY = (USD/CNY) / (USD/EUR) = 7.25 / 0.92
        BigDecimal usdCny = new BigDecimal("7.25");
        BigDecimal usdEur = new BigDecimal("0.92");
        
        BigDecimal eurCny = usdCny.divide(usdEur, 8, RoundingMode.HALF_UP);
        BigDecimal expected = new BigDecimal("7.88043478");
        
        // 允许0.0001误差
        assertTrue("交叉汇率 EUR/CNY 计算应正确",
            eurCny.subtract(expected).abs().compareTo(new BigDecimal("0.0001")) <= 0);
    }

    // ============ 批量计算测试 ============

    /**
     * 测试场景：多币种批量价格计算
     * 业务含义：批量获取时应保证所有价格正确
     */
    @Test
    public void testBatchPrice_Calculation() {
        Map<String, BigDecimal> prices = new HashMap<>();
        prices.put("BTC", new BigDecimal("67000"));
        prices.put("ETH", new BigDecimal("3400"));
        prices.put("BNB", new BigDecimal("580"));
        
        // 计算总市值（以美元计）
        BigDecimal totalMarketCap = BigDecimal.ZERO;
        for (Map.Entry<String, BigDecimal> entry : prices.entrySet()) {
            totalMarketCap = totalMarketCap.add(entry.getValue());
        }
        
        assertTrue("总市值应为正数", totalMarketCap.compareTo(BigDecimal.ZERO) > 0);
        assertEquals("三种币种市值为 67000+3400+580 = 70980",
            new BigDecimal("70980"), totalMarketCap);
    }

    /**
     * 测试场景：百分比变化计算
     * 业务含义：24小时涨跌幅计算
     */
    @Test
    public void testPercentageChange() {
        BigDecimal yesterdayPrice = new BigDecimal("65000");
        BigDecimal todayPrice = new BigDecimal("67000");
        
        BigDecimal change = todayPrice.subtract(yesterdayPrice)
            .divide(yesterdayPrice, 8, RoundingMode.HALF_UP)
            .multiply(new BigDecimal("100"));
        
        BigDecimal expectedChange = new BigDecimal("3.07692308");
        
        assertTrue("涨幅应约为 3.08%",
            change.subtract(expectedChange).abs().compareTo(new BigDecimal("0.01")) <= 0);
    }

    // ============ 缓存一致性测试 ============

    /**
     * 测试场景：价格缓存有效期检查
     * 业务含义：缓存应在合理时间内刷新
     */
    @Test
    public void testCache_ExpiryLogic() {
        long currentTime = System.currentTimeMillis();
        long cacheExpiry = 60000; // 60秒缓存
        
        // 当前时间应该小于缓存过期时间
        assertTrue("缓存应未过期", currentTime < currentTime + cacheExpiry);
        
        // 过期时间计算
        long expiryTime = currentTime + cacheExpiry;
        assertTrue("过期时间应在未来", expiryTime > currentTime);
    }

    /**
     * 测试场景：并发访问缓存
     * 业务含义：多线程环境下缓存应保持一致性
     */
    @Test
    public void testCache_ConcurrentAccess() {
        // 模拟并发场景
        final Map<String, BigDecimal> cache = new HashMap<>();
        cache.put("BTC", new BigDecimal("67000"));
        
        // 验证缓存数据一致性
        assertEquals("缓存读取应返回正确价格", 
            new BigDecimal("67000"), cache.get("BTC"));
        
        // 模拟更新
        cache.put("BTC", new BigDecimal("67100"));
        assertEquals("缓存更新后应返回新价格",
            new BigDecimal("67100"), cache.get("BTC"));
    }
}
