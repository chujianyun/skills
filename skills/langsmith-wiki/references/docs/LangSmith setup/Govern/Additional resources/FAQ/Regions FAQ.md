# Regions FAQ

> [!NOTE]
>
> See the [cloud architecture reference](../../../Cloud/Cloud%20%28SaaS%29.md#cloud-architecture-and-scalability) for additional details.

## Legal and compliance

#### *What privacy and data protection frameworks does LangSmith, including its regional instances, comply with?*

LangSmith complies with the General Data Protection Regulation (GDPR) and other laws and regulations applicable to the LangSmith service. We are also SOC 2 Type 2 certified and are HIPAA compliant. You can request more information about our security policies and posture at [trust.langchain.com](https://trust.langchain.com). If you would like to sign a Data Processing Addendum (DPA) with us, please contact support via [support.langchain.com](https://support.langchain.com).

For the security posture of LangSmith Engine, including its model subprocessors and data handling, see [Engine security](../../../../Engine/LangSmith%20Engine%20security.md).

#### *My company isn't based in a region, can I still have my data hosted there?*

Yes, you can host your LangSmith data in a supported regional instance independent of your location.

#### *Do you have a legal entity in the EU that we can contract with?*

We do not have a legal entity in the EU for customer contracting today.

#### *Do different legal terms apply if I choose a specific region?*

The terms are the same across supported cloud regions.

## Features

#### *How do I use a specific regional instance?*

Follow the [account and API key setup guide](../../../Account/Create%20an%20account%20and%20API%20key.md) to create an account and an API key. Make sure to choose the correct region in the region dropdown.

#### *Are there any functional differences between cloud-managed LangSmith regions?*

There may be a small delay between launches to each region depending on the feature. Besides that, supported cloud regions are functionally equivalent.

#### *Can an organization have workspaces in different regions?*

LangSmith does not support this at the moment, but if you are interested, please contact support via [support.langchain.com](https://support.langchain.com) and share your use case.

#### *Can I connect organizations across regions and share billing?*

LangSmith does not support this at the moment, but if you are interested, please contact support via [support.langchain.com](https://support.langchain.com) and share your use case.

#### *What data will be stored in my selected region?*

See the [cloud architecture reference](../../../Cloud/Cloud%20%28SaaS%29.md#cloud-architecture-and-scalability) for details.

#### *How can I see my organization's region?*

Open the LangSmith UI, and check the hostname in your browser's address bar. Each region has its own hostname:

<table>
  <thead>
    <tr>
      <th>Region</th>

      <th>
        Host
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>GCP US</td>

      <td>
        `smith.langchain.com`
      </td>
    </tr>

    <tr>
      <td>GCP EU</td>

      <td>
        `eu.smith.langchain.com`
      </td>
    </tr>

    <tr>
      <td>GCP APAC</td>

      <td>
        `apac.smith.langchain.com`
      </td>
    </tr>

    <tr>
      <td>AWS US</td>

      <td>
        `aws.smith.langchain.com`
      </td>
    </tr>

    <tr><td>Azure US</td>
    <td>`azure.smith.langchain.com`</td></tr>
  </tbody>
</table>

#### *Can I switch my organization between regions?*

We do not support migration between regions at this time, but if you are interested in this feature, please contact support via [support.langchain.com](https://support.langchain.com).

## Plans and pricing

#### *Are regional instances available on all LangSmith plans?*

Yes, you can sign up for supported regional instances on all plans including free plans.

#### *Is pricing different by region?*

No, pricing is the same across supported cloud regions.

#### *What currency is used for payment if I use a regional instance?*

All LangSmith plans are paid in USD.
