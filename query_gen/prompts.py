sys_prompt = """\
You are an AI assistant specialized in understanding Amazon's customer service guidelines and generating realistic customer queries. Your task is to analyze the provided Amazon help page content and create 10 unique, relevant questions that a typical customer might ask related to the given topic.

When processing the input, follow these steps:

1. Carefully read and comprehend the title and content of the Amazon help page provided.
2. Identify the key points, policies, and procedures mentioned in the guidelines.
3. Put yourself in the shoes of various Amazon customers who might encounter issues or have questions related to this topic.
4. Generate 10 distinct queries that:
   a. Reflect common customer concerns or confusions
   b. Cover different aspects of the guidelines
   c. Vary in complexity (from simple to more nuanced questions)
   d. Are phrased naturally, as a real customer would ask them
   e. Can be answered using the information provided in the guidelines
   f. Are not direct copies or paraphrases of the guideline content

5. Ensure that the queries are diverse and not repetitive.
6. Format your output as a JSON object with the original title and an array of 10 queries.

Remember:
- Focus on creating queries that real customers would ask, considering various scenarios and potential misunderstandings.
- Avoid using technical jargon unless it's commonly used by customers.
- Note that the typical customer might not aware of the existence of the guidelines provided to you. So, avoid making references to that in the customer's queries.
- Consider both straightforward and edge-case scenarios that customers might encounter.

Output JSON format:
{
    "title": "<title given by user>",
    "customer_queries": [
        "1. ...",
        "2. ...",
        ...
    ]
}

Your goal is to generate queries that accurately reflect what customers ask E-Commerce support agents in real life. The queries should encourage comprehensive use of the provided guidelines to formulate answers.
"""

sample_guidelines = """\
What is Exchange?

The Exchange Offer program on Amazon.in allows you to exchange your used product for a discount on a new product. For example, you can exchange your old products (AC, Washing Machine, Water Purifier, Television, Mobiles and so on,) by selecting the option "With Exchange" or "Exchange Your Old Phone/Product" option on the Product Detail page.
When placing the order for a new product that is eligible for the Exchange Offer on Amazon.in, you will be asked to provide details about the used product that you want to exchange. Based on the details you provide, an exchange value is calculated for your used product and applied as a discount on the new product during checkout. At the time of delivery of the new product, the delivery associate will verify and validate the used product with the details you provided at the time of placing the order. If the details match, the delivery associate will deliver your new product and pick up your used product. If the details don't match, or if the used product is not available for pick-up, the delivery of your new product will be suspended and your order may be cancelled.

Note:

    Exchange offer is currently available in select cities only. To check if is available at your selected address, enter your pincode in shipping address and the eligibility will be displayed.
    Before the delivery associate arrives, backup all your personal data, delete it from your used phone/tablet/laptop. Remove any memory card from the product.
    Remove any screen locks, iCloud locks or passwords from your exchange phone/tablet/laptop.
    Ensure your mobile/tablet/laptop has at least 50% charge so the delivery associate can conduct all the necessary tests without the battery running out.
    Before you handover the device for exchange, complete a full factory reset and reset your old device to ensure all personal data has been removed.
    Please note that the verification process will require the Rabbit Exchange app on used phone with customer logged in with the same Amazon account which was used to place the order. Kindly be available at the time of delivery or share the ordering account credentials with the intended recipient who will be present while exchanging the used device.
    For appliances such as, AC, Washing Machine, TV, Water Purifier, make sure these are uninstalled and ready for pickup.


Exchanging Mobiles

Note: To find your IMEI number to exchange your used mobile phone, dial *#06# from that phone. The IMEI number can also be found inside the battery compartment or in the phone settings or on the original packaging of the mobile phone.
Here is how exchange works for mobiles.

    At the time your new product is delivered, our delivery associate will check your used phone's physical and functional condition.
    For a fair evaluation, connect your used phone to the internet, remove any screen guard/tempered glass and phone cover (if any) and ensure the phone battery is at least 50%.
    Our delivery associate will run an automated test using your Amazon account on your used phone. This process can take up to 30 minutes. Please ensure you're logged into your Amazon account on your used phone.
    Note: Please note that the verification process will require the Rabbit Exchange app on used phone with customer logged in with the same Amazon account which was used to place the order. Kindly be available at the time of delivery or share the ordering account credentials with the intended recipient who will be present while exchanging the used device.
    Once the checks are completed:
        If your phone condition doesn't match as declared, you can still get a partial discount. You will need to pay the differential amount to the delivery associate.
        If your phone condition fails the verification, you will need to pay the exchange discount amount by Cash or Card and take delivery of your new phone. The exchange will be cancelled.


Exchanging Laptops/Tablets

Here is how exchange works for laptops/tablets.

    Before the delivery associate arrives, backup all your personal data and delete it from your used laptop/tablet. Remove the memory card (if any) from your laptop/tablet. Also remove any screen lock, iCloud lock or passwords.
    At the time of delivery of the new product, the delivery associate will assess the physical and functional condition of the used product.
    All the basic accessories and components for functioning of the device should also be handed over.


For TV, Refrigerator, Washing Machine and other appliances

Here is how exchange works for TVs, Washing Machines and other appliances.

    At the time of delivery, the delivery associate will check your used appliance's brand and model provided while placing the exchange order.
    Delivery associate might switch on the appliance by using appliance's power cable to check the working condition.
    Delivery associate will also check for major physical damage, spots/lines on TV screen, or signs of heavy rusting in refrigerators/washing machines/water heaters/microwaves/ACs.
    All the basic accessories and components for functioning of the device should also be handed over.


For Home Inverter Battery and Automotive Battery

    At the time of delivery, the delivery associate will check your used appliance's brand and model provided while placing the exchange order.
    Delivery associate will also check for major physical damage to the battery.
    All the basic accessories and components for functioning of the device should also be handed over.
"""
