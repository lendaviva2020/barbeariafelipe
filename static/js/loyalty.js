/**
 * Loyalty Program
 */

document.addEventListener('DOMContentLoaded', loadLoyaltyData);

async function loadLoyaltyData() {
    try {
        const response = await fetchAPI('/api/loyalty/me/');
        const data = await response.json();
        
        document.getElementById('pointsValue').textContent = data.points || 0;
        document.getElementById('tierBadge').textContent = getTierLabel(data.tier);
        
        // Progress to next tier
        const progress = calculateProgress(data.points, data.tier);
        document.getElementById('progressFill').style.width = `${progress}%`;
        
        const nextTierInfo = getNextTierInfo(data.tier, data.points);
        document.getElementById('nextTier').textContent = nextTierInfo;
    } catch (error) {
        console.error(error);
    }
}

function getTierLabel(tier) {
    const labels = { bronze: '🥉 Bronze', silver: '🥈 Silver', gold: '🥇 Gold' };
    return labels[tier] || 'Bronze';
}

function calculateProgress(points, tier) {
    if (tier === 'bronze') return (points / 200) * 100;
    if (tier === 'silver') return ((points - 200) / 300) * 100;
    return 100;
}

function getNextTierInfo(tier, points) {
    if (tier === 'bronze') return `Faltam ${200 - points} pontos para Silver`;
    if (tier === 'silver') return `Faltam ${500 - points} pontos para Gold`;
    return 'Você atingiu o nível máximo!';
}

